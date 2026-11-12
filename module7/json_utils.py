import json
import re
from typing import Any


def _strip_markdown(text: str) -> str:
    text = (text or "").strip()

    # Remove ```json ... ``` or ``` ... ```
    text = re.sub(r"^\s*```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```\s*$", "", text)

    return text.strip()


def _extract_candidates(text: str):
    candidates = [text]

    # Find possible JSON objects/arrays.
    object_start = text.find("{")
    object_end = text.rfind("}")
    if object_start >= 0 and object_end > object_start:
        candidates.append(text[object_start:object_end + 1])

    array_start = text.find("[")
    array_end = text.rfind("]")
    if array_start >= 0 and array_end > array_start:
        candidates.append(text[array_start:array_end + 1])

    # Remove duplicates while preserving order.
    result = []
    seen = set()

    for candidate in candidates:
        candidate = candidate.strip()
        if candidate and candidate not in seen:
            seen.add(candidate)
            result.append(candidate)

    return result


def _repair_with_json_repair(candidate: str):
    try:
        from json_repair import repair_json

        # return_objects=True directly returns a Python object.
        repaired = repair_json(candidate, return_objects=True)

        if repaired is not None:
            return repaired

    except Exception:
        pass

    return None


def _manual_cleanup(candidate: str) -> str:
    """
    Conservative cleanup for common LLM JSON mistakes.

    This does NOT modify normal JSON.
    """

    # Remove trailing commas before } or ].
    candidate = re.sub(r",\s*}", "}", candidate)
    candidate = re.sub(r",\s*]", "]", candidate)

    return candidate


def extract_json(text: str) -> Any:
    """
    Robustly extract JSON from an LLM response.

    Order:
      1. Strict JSON
      2. Extract JSON from surrounding text
      3. json-repair
      4. Conservative cleanup + strict JSON
      5. json-repair again
    """

    text = _strip_markdown(text)

    if not text:
        raise ValueError("LLM returned an empty response.")

    candidates = _extract_candidates(text)

    errors = []

    # ---------------------------------------------------------
    # 1. Normal JSON parsing
    # ---------------------------------------------------------
    for candidate in candidates:
        try:
            return json.loads(candidate)
        except json.JSONDecodeError as exc:
            errors.append(exc)

    # ---------------------------------------------------------
    # 2. json-repair
    # ---------------------------------------------------------
    for candidate in candidates:
        repaired = _repair_with_json_repair(candidate)

        if repaired is not None:
            return repaired

    # ---------------------------------------------------------
    # 3. Conservative cleanup
    # ---------------------------------------------------------
    for candidate in candidates:
        cleaned = _manual_cleanup(candidate)

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as exc:
            errors.append(exc)

    # ---------------------------------------------------------
    # 4. json-repair after cleanup
    # ---------------------------------------------------------
    for candidate in candidates:
        cleaned = _manual_cleanup(candidate)
        repaired = _repair_with_json_repair(cleaned)

        if repaired is not None:
            return repaired

    # ---------------------------------------------------------
    # Failure
    # ---------------------------------------------------------
    if errors:
        last_error = errors[-1]

        raise ValueError(
            f"Unable to parse Claude response as JSON. "
            f"JSON error: {last_error}. "
            f"Response preview: {text[:500]}"
        ) from last_error

    raise ValueError(
        f"No JSON object or array found in Claude response. "
        f"Response preview: {text[:500]}"
    )