package com.c2o.cv2offer.service.impl;

import com.c2o.cv2offer.dto.InterviewSimulateRequestDTO;
import com.c2o.cv2offer.exception.BusinessException;
import com.c2o.cv2offer.model.ApiResponse;
import com.c2o.cv2offer.service.InterviewService;
import com.c2o.cv2offer.util.PythonApiCaller;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.Base64;
import java.util.HashMap;
import java.util.Map;

@Service
public class InterviewServiceImpl implements InterviewService {

    @Autowired
    private PythonApiCaller pythonApiCaller;

    @Override
    public ApiResponse simulateInterview(InterviewSimulateRequestDTO request) {
        try {
            // 验证请求参数
            validateRequest(request);
            
            // 准备请求数据
            Map<String, Object> requestData = new HashMap<>();
            
            // 处理简历文件（如果有）
            MultipartFile resumeFile = request.getFile();
            if (resumeFile != null && !resumeFile.isEmpty()) {
                // 验证文件格式
                String filename = resumeFile.getOriginalFilename();
                if (filename != null && !filename.toLowerCase().endsWith(".pdf")) {
                    throw new BusinessException("只支持PDF格式的简历文件");
                }
                
                // 将PDF文件转换为Base64编码
                byte[] fileContent = resumeFile.getBytes();
                String encodedString = Base64.getEncoder().encodeToString(fileContent);
                requestData.put("resume_pdf_base64", encodedString);
                requestData.put("filename", filename);
            }
            
            // 添加其他参数
            requestData.put("job_position", request.getPosition());
            
            if (request.getCompany() != null && !request.getCompany().isEmpty()) {
                requestData.put("company_name", request.getCompany());
            }
            
            requestData.put("interview_type", request.getInterviewType());
            requestData.put("difficulty", request.getDifficulty());
            
            // 如果是继续会话，添加会话ID和用户回答
            if (request.getSessionId() != null && !request.getSessionId().isEmpty()) {
                requestData.put("session_id", request.getSessionId());
                
                if (request.getUserAnswer() == null || request.getUserAnswer().trim().isEmpty()) {
                    throw new BusinessException("继续会话时，用户回答不能为空");
                }
                
                requestData.put("user_answer", request.getUserAnswer());
            }

            // 调用Python API进行面试模拟
            String response = pythonApiCaller.callInterviewApi(requestData);
            
            // 返回API响应
            return ApiResponse.success(response);
        } catch (BusinessException e) {
            return ApiResponse.error(e.getMessage());
        } catch (IOException e) {
            return ApiResponse.error("文件处理失败: " + e.getMessage());
        } catch (Exception e) {
            return ApiResponse.error("面试模拟失败: " + e.getMessage());
        }
    }
    
    /**
     * 验证请求参数
     */
    private void validateRequest(InterviewSimulateRequestDTO request) {
        if (request == null) {
            throw new BusinessException("请求不能为空");
        }
        
        if (request.getPosition() == null || request.getPosition().trim().isEmpty()) {
            throw new BusinessException("面试职位不能为空");
        }
        
        if (request.getInterviewType() == null || request.getInterviewType().trim().isEmpty()) {
            throw new BusinessException("面试类型不能为空");
        }
    }
}