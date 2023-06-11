# llama.cpp serve Playground🦙

A very simple playground inpired on Open-AI playground for llama.cpp http server usage.

server.cpp: https://github.com/ggerganov/llama.cpp/blob/master/examples/server/server.cpp

### Screenshot
 ![Image](https://i.ibb.co/6gJXCCD/screenshot.png)

### Configure proxy address

Edit the vite.config.ts and change the "target" value for the llama.cpp server ip. By default serve.cpp uses http://127.0.0.1:8080.

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