# Rode essa API via docker em qualquer plataforma. Uma opção simples e gratuita é roda-la via Play With Docker através da imagem publicada no Dockerhub
> [!NOTE]
> ## Passo 1: 
> * Acesse https://labs.play-with-docker.com/ e crie uma instância
> ## Passo 2: 
> * Execute o comando a seguir:
> ```
>   docker run -it -p 8080:8080 eumagnun/banco-demo-api:latest
> ```
> * A OAS (Open API Specification) estará disponivel na url exibida, no path /docs. COnforme exemplo abaixo:
> * http://ip172-18-0-20-cop6tva91nsg00e5jtng-8080.direct.labs.play-with-docker.com/docs
