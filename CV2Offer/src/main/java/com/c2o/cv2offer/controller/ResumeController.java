package com.c2o.cv2offer.controller;

import com.c2o.cv2offer.dto.ResumeOptimizeRequestDTO;
import com.c2o.cv2offer.model.ApiResponse;
import com.c2o.cv2offer.service.ResumeService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import jakarta.validation.Valid;

@RestController
@RequestMapping("/api/resume")
public class ResumeController {

    @Autowired
    private ResumeService resumeService;

    @PostMapping("/optimize")
    public ApiResponse optimizeResume(@Valid ResumeOptimizeRequestDTO request) {
        return resumeService.optimizeResume(request);
    }
}