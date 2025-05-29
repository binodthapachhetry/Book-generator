#  📚 Book Generator

## 📄 Description

Generate a picture book from a single prompt using [OpenAI's new function calling](https://openai.com/blog/function-calling-and-other-api-updates) and [Replicate's API](https://replicate.com/) for Google's Imagen-4. Check [example.pdf](https://github.com/binodthapachhetry/Book-generator/blob/main/example.pdf) or watch the video below for a peek at the output. 

Built with [LangChain](https://github.com/hwchase17/langchain), and [Replicate](https://replicate.com/).

## :tv: Demo
https://github.com/e-johnstonn/FableForge/assets/30129211/f9523905-342e-4a33-914d-acd13bd168ec


## 🛠 Install
1. Clone the repository
2. Install requirements.txt
3. Set up your OpenAI and Replicate API keys in `keys.env` - More on this below
4. Run `streamlit run main.py` to start the app!


## 🖼️ Replicate Setup
A Replicate API key is necessary for this app. To get one, go to the [Replicate website](https://replicate.com/) and create an account, then take your API key and put it in `keys.env`. Replicate provides free image generation for new users. 

## 📐Architecture

![architecture](https://github.com/binodthapachhetry/Book-generator/blob/main/ARCHITECTURE.md)


## Improvements
- This demo uses Replicate for image generation due to its ease of use. Connect it to your own text-to-image model (local or cloud-based) for better results. I recommend some combination of [Diffusers](https://github.com/huggingface/diffusers) and [FastAPI](https://github.com/tiangolo/fastapi) as a starting point.


## License
[MIT License](LICENSE)





