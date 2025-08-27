FROM eclipse-temurin:21.0.8_9-jre-jammy
WORKDIR /app
RUN cd /app
COPY ./target/*.jar app.jar
ENTRYPOINT ["java","-jar","app.jar"]
EXPOSE 7000
