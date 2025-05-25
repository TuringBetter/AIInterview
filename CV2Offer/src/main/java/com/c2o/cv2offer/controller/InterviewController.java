package com.c2o.cv2offer.controller;

import com.c2o.cv2offer.dto.InterviewSimulateRequestDTO;
import com.c2o.cv2offer.model.ApiResponse;
import com.c2o.cv2offer.service.InterviewService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import jakarta.validation.Valid;

@RestController
@RequestMapping("/api/interview")
public class InterviewController {

    @Autowired
    private InterviewService interviewService;

    @PostMapping("/simulate")
    public ApiResponse simulateInterview(@Valid InterviewSimulateRequestDTO request) {
        return interviewService.simulateInterview(request);
    }
}