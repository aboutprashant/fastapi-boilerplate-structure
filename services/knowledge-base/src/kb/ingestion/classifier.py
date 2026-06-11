from dataclasses import dataclass


@dataclass(frozen=True)
class ClassificationResult:
    detected_doc_type: str
    verdict: str


class MockDocumentClassifier:
    async def classify(self, declared_doc_type: str, first_pages_text: str) -> ClassificationResult:
        text = first_pages_text.lower()
        if "progress" in text:
            detected = "progress_report"
        elif "donor" in text or "agreement" in text:
            detected = "donor_agreement"
        elif "monitoring" in text or "evaluation" in text:
            detected = "me_plan"
        else:
            detected = declared_doc_type
        return ClassificationResult(
            detected_doc_type=detected,
            verdict="green" if detected == declared_doc_type else "orange",
        )
