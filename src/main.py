from gradio_app import demo

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", 
                server_port=8000, 
                share=False,
                show_api=False)
