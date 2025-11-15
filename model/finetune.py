"""Script de fine-tuning LoRA pour A Maestra.

Ce script prépare l'entraînement d'un adaptateur LoRA sur notre dataset
instruction/réponse afin de spécialiser un modèle de base à la langue corse.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict

import torch
from datasets import Dataset, load_dataset
from peft import LoraConfig, PeftModel, get_peft_model
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments,
)

# Modèle de base instruct multilingue (licence permissive) retenu pour Maestra.
# IMPORTANT : conserver ce modèle de référence pour la reproductibilité du fine-tune.
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"

DATA_PATH = Path("data/training_examples.jsonl")
CHECKPOINT_DIR = Path("model/checkpoints")
ADAPTER_DIR = CHECKPOINT_DIR / "adapter"
PROMPT_TEMPLATE = "<s>Instruction: {instruction}\nRéponse: {response}</s>"
INFERENCE_TEMPLATE = "<s>Instruction: {instruction}\nRéponse:"

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def load_training_dataset(path: Path = DATA_PATH) -> Dataset:
    """Charge le dataset JSONL d'instruction-tuning."""

    if not path.exists():
        raise FileNotFoundError(f"Dataset introuvable: {path}")

    dataset = load_dataset("json", data_files=str(path), split="train")
    logger.info("Dataset chargé avec %d exemples", len(dataset))
    return dataset


def build_prompt(example: Dict[str, Any]) -> Dict[str, str]:
    """Construit un prompt lisible combinant instruction et réponse."""

    instruction = example.get("instruction", "").strip()
    response = example.get("response", "").strip()
    # On entraîne le modèle comme un assistant : l'utilisateur pose une question
    # ("instruction"), le modèle doit répondre en corse / expliquer.
    # IMPORTANT : garder ce format EXACT pour la génération plus tard.
    prompt = PROMPT_TEMPLATE.format(instruction=instruction, response=response)
    return {"text": prompt, "instruction": instruction, "response": response}


def tokenize_dataset(dataset: Dataset, tokenizer) -> Dataset:
    """Applique le tokenizer et génère les labels pour l'entraînement auto-régressif."""

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    def _tokenize(batch: Dict[str, Any]) -> Dict[str, Any]:
        tokenized = tokenizer(
            batch["text"],
            truncation=True,
            padding="longest",
        )
        tokenized["labels"] = tokenized["input_ids"].copy()
        return tokenized

    tokenized_dataset = dataset.map(
        _tokenize,
        batched=True,
        remove_columns=dataset.column_names,
    )
    logger.info("Dataset tokenizé.")
    return tokenized_dataset


def prepare_model() -> torch.nn.Module:
    """Charge le modèle de base et applique la configuration LoRA."""

    logger.info("Chargement du modèle de base %s", MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        device_map="auto",
        torch_dtype="auto",
    )

    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],  # TODO: ajuster si besoin
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    return model


def train() -> None:
    """Lance l'entraînement LoRA sur le dataset Maestra."""

    raw_dataset = load_training_dataset()
    processed_dataset = raw_dataset.map(build_prompt)

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    tokenizer.padding_side = "right"
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    tokenized_dataset = tokenize_dataset(processed_dataset, tokenizer)

    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)

    training_args = TrainingArguments(
        output_dir=str(CHECKPOINT_DIR),
        num_train_epochs=3,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        logging_steps=10,
        save_steps=200,
        save_total_limit=2,
        fp16=True,  # TODO: passer à bf16 selon le GPU disponible
        remove_unused_columns=False,
        report_to=[],
        evaluation_strategy="no",
    )

    model = prepare_model()

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
        data_collator=data_collator,
    )

    logger.info("Démarrage de l'entraînement LoRA...")
    trainer.train()

    logger.info("Enregistrement de l'adaptateur LoRA dans %s", ADAPTER_DIR)
    ADAPTER_DIR.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(str(ADAPTER_DIR))
    tokenizer.save_pretrained(str(ADAPTER_DIR))
    logger.info("Entraînement terminé.")


def load_model_with_adapter(adapter_dir: Path | str = ADAPTER_DIR) -> torch.nn.Module:
    """Recharge le modèle de base et l'adaptateur LoRA pour l'inférence."""

    adapter_dir = Path(adapter_dir)

    if not adapter_dir.exists():
        raise FileNotFoundError(
            f"Adaptateur introuvable dans {adapter_dir}. Lancez d'abord l'entraînement."
        )

    base_model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        device_map="auto",
        torch_dtype="auto",
    )
    model = PeftModel.from_pretrained(base_model, str(adapter_dir))
    model.eval()
    return model


def generate_demo(
    user_instruction: str,
    max_new_tokens: int = 128,
    adapter_dir: Path | str = ADAPTER_DIR,
) -> str:
    """Génère une réponse de démonstration avec le modèle fine-tuné."""

    # Ceci sert à tester le modèle fine-tuné localement après entraînement.
    adapter_dir = Path(adapter_dir)
    if not adapter_dir.exists():
        raise FileNotFoundError(
            "Adaptateur LoRA introuvable. Lancez l'entraînement avant de tester."
        )

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    prompt = INFERENCE_TEMPLATE.format(instruction=user_instruction.strip())
    inputs = tokenizer(prompt, return_tensors="pt")

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        device_map="auto",
        torch_dtype="auto",
    )
    model = PeftModel.from_pretrained(model, str(adapter_dir))
    model.eval()

    device = model_device()
    model.to(device)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        generated = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id,
        )

    decoded = tokenizer.decode(generated[0], skip_special_tokens=True)
    response = decoded.replace(prompt, "").strip()
    return response or "(Réponse vide)"


def model_device() -> torch.device:
    """Détermine le device à utiliser (GPU si disponible, sinon CPU)."""

    if torch.cuda.is_available():
        return torch.device("cuda")
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


if __name__ == "__main__":
    # Exécuter `python model/finetune.py` lancera l'entraînement LoRA complet.
    train()
