from nltk.chat.util import Chat, reflections

pairs = [
    ["my name is (.*)", ["Hi %1, how can I help you?"]],
    ["(hi|hello|hey)", ["Hello, how can I assist you?"]],
    ["(.*) in (.*) is fun", ["%1 in %2 is indeed fun!"]],
    ["(.*?) (location|city) ?", ["I'm a chatbot, so I don't have a physical presence anywhere!"]],
]

chatbot = Chat ( pairs, reflections )
chatbot.converse ()
