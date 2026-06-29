"""Question-generation tools used by the question generator agent."""

from registery.decorators import register_tool


@register_tool(tags=["question_generation"])
def generate_question(
	topic: str,
	difficulty: str,
	question_text: str,
	options: list,
	correct_answer: str,
) -> dict:
	"""Package a question into a single structured payload."""
	return {
		"topic": topic,
		"difficulty": difficulty,
		"question_text": question_text,
		"options": options,
		"correct_answer": correct_answer,
	}


@register_tool(tags=["question_generation"])
def validate_question(question: dict) -> dict:
	"""Validate that a question payload is complete and well-formed."""
	errors = []

	required_fields = ["topic", "difficulty", "question_text", "options", "correct_answer"]
	for field in required_fields:
		if field not in question or question[field] in (None, "", []):
			errors.append(f"Missing or empty field: {field}")

	options = question.get("options")
	if not isinstance(options, list):
		errors.append("options must be a list")
	elif len(options) != 4:
		errors.append("options must contain exactly 4 items")
	elif question.get("correct_answer") not in options:
		errors.append("correct_answer must match one of the options")

	if errors:
		return {"valid": False, "errors": errors}

	return {"valid": not errors, "errors": errors}


@register_tool(tags=["question_generation"], terminal=True)
def terminate(question: dict) -> dict:
	"""Return the final validated question and stop the agent loop."""
	return question
