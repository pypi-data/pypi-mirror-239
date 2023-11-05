import uvicorn

def main():
    uvicorn.run("main:app", 
                port=8070, 
                log_level="debug", 
                workers=1,
                limit_concurrency=1)

if __name__ == "__main__":
    main()
