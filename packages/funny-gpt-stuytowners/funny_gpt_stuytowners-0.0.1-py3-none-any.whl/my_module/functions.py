import openai

def llm(question):
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=[
        {"role": "user", "content": question},
        ],
        max_tokens=200,
        temperature=0.99
    )
    answer = response['choices'][0]['message']['content']

    return answer

preset = "You are the most chill cs professor in the world, Professor Foo Barstein. You are talking to me, a student in your class."

def gptchat(type=None, subject=None, preset=preset):
    if (type=="joke"):
        if (subject):
            response=llm(preset + "tell me a funny joke about " + subject)
        else:
            response=llm(preset + "tell me a funny joke")
    elif (type=="haiku"):
        if (subject):
            response=llm(preset + "tell me a haiku about " + subject)
        else:
            response=llm(preset + "tell me a haiku")
    elif (type=="compliment"):
        if (subject):
            response=llm(preset + "tell me a compliment about " + subject)
        else:
            response=llm(preset + "tell me a compliment")
    elif (type=="email"):
        if (subject):
            response=llm(preset + "write an email about " + subject)
        else:
            response=llm(preset + "write a random email to send to my boss")
    else:
        if (subject):
            response=llm(preset + subject)
        else:
            response=llm(preset + "say something random")
    # print(response)
    return response

def cowtalk(type='joke'):
    words = gptchat(type).split()
    moo_words = ' moo '.join(words)  # Insert 'moo' between each word
    print(moo_words)
    

def onewordperline(type=None):
    words = gptchat(type).split()  # Split the response into words
    max_word_length = max(len(word) for word in words)

    for i in range(max_word_length):
        for word in words:
            if i < len(word):
                print(word[i], end=' ')
            else:
                print('  ', end=' ')  # Print two spaces for alignment
        print()

def changepreset():
    new_preset = input("Enter the new preset: ")
    global preset  # Use the 'preset' variable defined outside the function
    preset = new_preset

# this changes the preset phrase up top, yay!

def main():
    print(onewordperline())

if __name__ == "__main__":
    main()