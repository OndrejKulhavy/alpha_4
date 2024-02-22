@app.route('/messages')
def get_all_messages():
    raise NotImplementedError("Get all messages")


@app.route('/send', methods=['GET'])
def greet():
    message = request.args.get('message')
    if message is None:
        return "Missing atribute message"
    raise NotImplementedError("Missing logic for sending a message")
