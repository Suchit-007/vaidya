import uuid
from datetime import datetime
from typing import Dict, Any

def generate_fhir_bundle(analysis_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates an HL7 FHIR R4 Bundle (Collection) containing a Composition resource
    for the Ayurvedic clinical analysis.
    """
    bundle_id = str(uuid.uuid4())
    composition_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat() + "Z"
    
    entities_text = ", ".join([f"{e['term']} ({e['definition']})" for e in analysis_data.get("extracted_entities", [])])
    
    bundle = {
        "resourceType": "Bundle",
        "id": bundle_id,
        "type": "collection",
        "timestamp": now,
        "entry": [
            {
                "fullUrl": f"urn:uuid:{composition_id}",
                "resource": {
                    "resourceType": "Composition",
                    "id": composition_id,
                    "status": "final",
                    "type": {
                        "coding": [
                            {
                                "system": "http://loinc.org",
                                "code": "11488-4",
                                "display": "Consult Note"
                            }
                        ],
                        "text": "Ayurvedic Clinical Analysis"
                    },
                    "subject": {
                        "display": "Anonymous Patient"
                    },
                    "date": now,
                    "author": [
                        {
                            "display": "Vaidya.ai Intelligence Engine"
                        }
                    ],
                    "title": f"Ayurvedic Analysis: {analysis_data.get('source_text', 'General Query')}",
                    "section": [
                        {
                            "title": "Clinical Summary",
                            "code": {
                                "coding": [
                                    {
                                        "system": "http://loinc.org",
                                        "code": "55112-7",
                                        "display": "Summary of clinical findings"
                                    }
                                ]
                            },
                            "text": {
                                "status": "generated",
                                "div": f"<div xmlns=\"http://www.w3.org/1999/xhtml\">"
                                       f"<p><strong>Analysis:</strong> {analysis_data.get('answer', '')}</p>"
                                       f"<p><strong>Confidence:</strong> {analysis_data.get('confidence_tier', 'UNKNOWN')}</p>"
                                       f"<p><strong>Terminology:</strong> {entities_text}</p>"
                                       f"</div>"
                            }
                        }
                    ]
                }
            }
        ]
    }
    
    return bundle
