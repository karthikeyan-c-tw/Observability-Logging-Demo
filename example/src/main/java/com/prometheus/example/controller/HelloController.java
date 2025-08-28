package com.prometheus.example.controller;

import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
@Slf4j
public class HelloController {

    @GetMapping("/message/{msg}")
    public String hello(@PathVariable(name="msg") String message) {
        log.info("message: {}", message);
        if("hello".equalsIgnoreCase(message)) {
            log.error("message is invalid");
            return null;
        }
        return "Hello! " + message;
    }
}
