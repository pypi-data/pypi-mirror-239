from qualtop_llmapi.main import app
import uvicorn

def main():
    uvicorn.run(app, 
                port=8070, 
                log_level="debug", 
                workers=1)

if __name__ == "__main__":
    main()
