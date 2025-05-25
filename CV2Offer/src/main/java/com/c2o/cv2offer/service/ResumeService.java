package com.c2o.cv2offer.service;

import com.c2o.cv2offer.dto.ResumeOptimizeRequestDTO;
import com.c2o.cv2offer.model.ApiResponse;

public interface ResumeService {
    ApiResponse optimizeResume(ResumeOptimizeRequestDTO request);
}