package com.c2o.cv2offer.service;

import com.c2o.cv2offer.dto.InterviewSimulateRequestDTO;
import com.c2o.cv2offer.model.ApiResponse;

public interface InterviewService {
    ApiResponse simulateInterview(InterviewSimulateRequestDTO request);
}