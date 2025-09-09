package com.prometheus.example.service;

import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.MeterRegistry;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class MetricsService {

    private final MeterRegistry meterRegistry;

    public void recordSuccess() {
        Counter.builder("message_api_requests_total")
                .tag("status", "success")
                .register(meterRegistry)
                .increment();
    }

    public void recordFailure() {
        Counter.builder("message_api_errors_total")
                .tag("status", "failure")
                .register(meterRegistry)
                .increment();
    }
}
