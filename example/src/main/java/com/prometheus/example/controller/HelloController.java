package com.prometheus.example.controller;

import com.prometheus.example.service.MetricsService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

@RestController
@Slf4j
@RequiredArgsConstructor
public class HelloController {

    private final MetricsService metricsService;

    @GetMapping("/message/{msg}")
    public String hello(@PathVariable(name="msg") String message) {
        log.info("message: {}", message);
        if("hello".equalsIgnoreCase(message)) {
            log.error("message is invalid");
            metricsService.recordFailure();
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "message not found");
        }
        metricsService.recordSuccess();
        return "Hello! " + message;
    }
}
