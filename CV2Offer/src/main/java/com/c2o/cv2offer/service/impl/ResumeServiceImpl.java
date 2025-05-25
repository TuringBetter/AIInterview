package com.c2o.cv2offer.service.impl;

import com.c2o.cv2offer.dto.ResumeOptimizeRequestDTO;
import com.c2o.cv2offer.exception.BusinessException;
import com.c2o.cv2offer.model.ApiResponse;
import com.c2o.cv2offer.service.ResumeService;
import com.c2o.cv2offer.util.PythonApiCaller;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.Base64;
import java.util.HashMap;
import java.util.Map;

@Service
public class ResumeServiceImpl implements ResumeService {

    @Autowired
    private PythonApiCaller pythonApiCaller;

    @Override
    public ApiResponse optimizeResume(ResumeOptimizeRequestDTO request) {
        try {
            // 验证请求参数
            validateRequest(request);
            
            // 获取DTO中的文件和其他参数
            MultipartFile resumeFile = request.getFile();
            String jobPosition = request.getTargetPosition();
            String targetCompany = request.getTargetCompany();
            String additionalInfo = request.getAdditionalInfo();
            
            // 将PDF文件转换为Base64编码
            byte[] fileContent = resumeFile.getBytes();
            String encodedString = Base64.getEncoder().encodeToString(fileContent);

            // 准备请求数据
            Map<String, Object> requestData = new HashMap<>();
            requestData.put("resume", encodedString);
            requestData.put("position", jobPosition);
            requestData.put("company", targetCompany);
            requestData.put("requirements", additionalInfo);
            requestData.put("filename", resumeFile.getOriginalFilename());

            // 添加其他参数
            if (jobPosition != null && !jobPosition.isEmpty()) {
                requestData.put("job_position", jobPosition);
            }
            
            if (targetCompany != null && !targetCompany.isEmpty()) {
                requestData.put("target_company", targetCompany);
            }
            
            if (additionalInfo != null && !additionalInfo.isEmpty()) {
                requestData.put("additional_info", additionalInfo);
            }

            //待修改 调用Python API进行简历修改
            String response = pythonApiCaller.callResumeApi(requestData);
            
            // 返回API响应
            return ApiResponse.success(response);
        } catch (BusinessException e) {
            return ApiResponse.error(e.getMessage());
        } catch (IOException e) {
            return ApiResponse.error("文件处理失败: " + e.getMessage());
        } catch (Exception e) {
            return ApiResponse.error("简历修改失败: " + e.getMessage());
        }
    }
    
    /**
     * 验证请求参数
     */
    private void validateRequest(ResumeOptimizeRequestDTO request) {
        if (request == null) {
            throw new BusinessException("请求不能为空");
        }
        
        if (request.getFile() == null || request.getFile().isEmpty()) {
            throw new BusinessException("简历文件不能为空");
        }
        
        String filename = request.getFile().getOriginalFilename();
        if (filename == null || !filename.toLowerCase().endsWith(".pdf")) {
            throw new BusinessException("只支持PDF格式的简历文件");
        }
        
        if (request.getTargetPosition() == null || request.getTargetPosition().trim().isEmpty()) {
            throw new BusinessException("目标职位不能为空");
        }
    }
}