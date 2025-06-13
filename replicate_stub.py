import base64, requests, uuid, os

def run(_model_id, input):
    prompt = input["prompt"]
    seed   = input.get("seed", 0)
    resp = requests.post(os.environ["SD_ENDPOINT"] + "/txt2img",
                         json={"prompt": prompt, "seed": seed}, timeout=120)
    b64 = resp.json()["image"]
    fname = f"/tmp/{uuid.uuid4()}.png"
    with open(fname, "wb") as f:
        f.write(base64.b64decode(b64))
    return fname     # replicate.run originally returns a URL; returning a path still satisfies downstream code
