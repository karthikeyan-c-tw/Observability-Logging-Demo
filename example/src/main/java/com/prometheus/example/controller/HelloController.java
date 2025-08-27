package com.prometheus.example.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HelloController {

    @GetMapping("/message/{msg}")
    public String hello(@PathVariable(name="msg") String message) {
        return "Hello! " + message;
    }
}
