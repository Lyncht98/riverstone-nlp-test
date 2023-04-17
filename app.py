from shiny import ui, render, App
import socket

app_ui = ui.page_fluid(
    ui.input_slider("n", "N", 0, 100, 40),
    ui.output_text_verbatim("txt"),
)

def server(input, output, session):
    @output
    @render.text
    def txt():
        return f"n*2 is {input.n() * 2}"

# This is a shiny.App object. It must be named `app`.
app = App(app_ui, server)

def print_local_address():
    # Get the local address of the computer
    local_address = socket.gethostbyname(socket.gethostname())

    # Print the local address
    print("My local address is:", local_address)

if __name__ == "__main__":

# Call the print_local_address() function
    print_local_address()
    app.run()