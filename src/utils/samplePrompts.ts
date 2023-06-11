import { reactive  } from 'vue'

const prompts = {
    "<Click here>":"",
    "Default":"Hello World, how are",
    "Text Translation":"Spanish:La Tierra (del latín Terra,17​ deidad romana equivalente a Gea, diosa griega de la feminidad y la fecundidad) es un planeta del sistema solar que gira alrededor de su estrella —el Sol— en la tercera órbita más interna. Es el más denso y el quinto mayor de los ocho planetas del sistema solar. También es el mayor de los cuatro terrestres o rocosos.\n\nEnglish:",
    "Chat Style":"This is a chat between a human and assistant\n### Human:Hello.\n### Assistant:Hello Human\n### Human:",
    "Summarization":"Text:Apollo 11 (July 16–24, 1969) was the American spaceflight that first landed humans on the Moon. Commander Neil Armstrong and lunar module pilot Buzz Aldrin landed the Apollo Lunar Module Eagle on July 20, 1969, at 20:17 UTC, and Armstrong became the first person to step onto the Moon's surface six hours and 39 minutes later, on July 21 at 02:56 UTC. Aldrin joined him 19 minutes later, and they spent about two and a quarter hours together exploring the site they had named Tranquility Base upon landing. Armstrong and Aldrin collected 47.5 pounds (21.5 kg) of lunar material to bring back to Earth as pilot Michael Collins flew the Command Module Columbia in lunar orbit, and were on the Moon's surface for 21 hours, 36 minutes before lifting off to rejoin Columbia.\n\n\ntldr:",
}


let samplePrompts = reactive({})

Object.assign(samplePrompts,prompts)

export { samplePrompts }