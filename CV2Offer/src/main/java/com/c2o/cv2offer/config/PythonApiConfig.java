package com.c2o.cv2offer.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class PythonApiConfig {

    @Value("${python.scripts.path:./python}")
    private String pythonScriptsPath;

    @Value("${python.resume.script:resume_optimizer.py}")
    private String resumeScript;

    @Value("${python.interview.script:interview_simulator.py}")
    private String interviewScript;

    // 保留这些方法以兼容现有代码
    public String getResumeEndpoint() {
        return pythonScriptsPath + "/" + resumeScript;
    }

    public String getInterviewEndpoint() {
        return pythonScriptsPath + "/" + interviewScript;
    }

    public String getPythonScriptsPath() {
        return pythonScriptsPath;
    }

    public String getResumeScript() {
        return resumeScript;
    }

    public String getInterviewScript() {
        return interviewScript;
    }
}