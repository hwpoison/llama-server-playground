# llama.cpp server Playground🦙

A very simple playground inpired on Open-AI playground for llama.cpp http server usage.
If you want to handle multiple instances subprocess you can use the backend, but it is not necessary for and stanlone server.cpp execution.

More information about server.cpp: https://github.com/ggerganov/llama.cpp/tree/master/examples/server

### Screenshot
 ![Image](https://i.ibb.co/QXB89gK/screenshot.png)

### Configure proxy address

Edit the vite.config.ts and change the "target" value for the llama.cpp server ip. By default serve.cpp connects to backend proxy default ip http://127.0.0.1:5000 to the endpoint /api.

### How to run
#### Install dependences
```
npm install
```

#### Launch server
```
npm run dev
```

#### Compiles and minifies for production
```
npm run build
```