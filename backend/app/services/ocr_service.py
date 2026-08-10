import json

from fastapi import HTTPException, status

from backend.app.core.config import settings


def extract_text_from_image_bytes(image_bytes: bytes) -> str:
    if not settings.rapidapi_key:
        # Fallback text for development when no OCR API key is configured.
        return (
            "Patient should take 1 tablet Paracetamol 500mg twice daily for 5 days. "
            "Monitor fever and contact the doctor if symptoms worsen."
        )

    import http.client

    conn = http.client.HTTPSConnection(settings.rapidapi_host)
    boundary = "----011000010111000001101001"
    payload = (
        f"--{boundary}\r\n"
        "Content-Disposition: form-data; name=\"srcImg\"; filename=\"image.jpg\"\r\n"
        "Content-Type: image/jpeg\r\n\r\n"
    ).encode("utf-8") + image_bytes + f"\r\n--{boundary}--\r\n".encode("utf-8")

    headers = {
        "x-rapidapi-key": settings.rapidapi_key,
        "x-rapidapi-host": settings.rapidapi_host,
        "Content-Type": f"multipart/form-data; boundary={boundary}",
    }

    conn.request("POST", "/recognize/", payload, headers)
    response = conn.getresponse()
    body = response.read()

    if response.status != 200:
        raise HTTPException(
            status_code=response.status,
            detail=f"OCR service request failed: {body.decode('utf-8', errors='ignore')}",
        )

    try:
        data = json.loads(body.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Invalid OCR response: {exc}",
        )

    text = data.get("value", "")
    if not text:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="OCR did not return any text from the uploaded image.",
        )

    return text.strip()
