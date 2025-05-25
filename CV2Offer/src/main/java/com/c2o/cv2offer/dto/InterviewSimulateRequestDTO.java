package com.c2o.cv2offer.dto;

import lombok.Data;
import org.springframework.web.multipart.MultipartFile;
import jakarta.validation.constraints.NotBlank;

@Data
public class InterviewSimulateRequestDTO {
    
    private MultipartFile file;
    
    @NotBlank(message = "面试职位不能为空")
    private String position;
    
    private String company;
    
    @NotBlank(message = "面试类型不能为空")
    private String interviewType;
    
    private String difficulty = "中等"; // 默认值
    
    private String userAnswer;
    
    private String sessionId;
}