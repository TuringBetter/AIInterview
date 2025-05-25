package com.c2o.cv2offer.dto;

import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.NotBlank;
import lombok.Data;
import org.springframework.web.multipart.MultipartFile;

@Data
public class ResumeOptimizeRequestDTO {
    
    @NotNull(message = "简历文件不能为空")
    private MultipartFile file;
    
    @NotBlank(message = "目标职位不能为空")
    private String targetPosition;
    
    private String targetCompany;
    
    private String additionalInfo;
}