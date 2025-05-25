package com.c2o.cv2offer.util;

import com.c2o.cv2offer.config.PythonApiConfig;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.file.Paths;
import java.util.Map;
import java.util.stream.Collectors;

@Component
public class PythonApiCaller {

    @Autowired
    private PythonApiConfig pythonApiConfig;

    /**
     * 调用Python简历优化脚本
     * @param requestData 请求数据
     * @return 处理结果
     */
    public String callResumeApi(Map<String, Object> requestData) {
        try {
            // 构建Python脚本路径
            // 修改callResumeApi方法中的脚本路径获取
            String pythonScript = Paths.get(pythonApiConfig.getPythonScriptsPath(), pythonApiConfig.getResumeScript()).toString();

            // 构建命令参数
            StringBuilder cmdArgs = new StringBuilder();
            for (Map.Entry<String, Object> entry : requestData.entrySet()) {
                cmdArgs.append(" --").append(entry.getKey()).append("=").append(entry.getValue());
            }

            // 执行Python脚本
            Process process = Runtime.getRuntime().exec("python " + pythonScript + cmdArgs.toString());

            // 获取脚本输出
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String result = reader.lines().collect(Collectors.joining("\n"));

            // 获取脚本错误输出
            BufferedReader errorReader = new BufferedReader(new InputStreamReader(process.getErrorStream()));
            String errorOutput = errorReader.lines().collect(Collectors.joining("\n"));

            // 记录错误输出
            if (!errorOutput.isEmpty()) {
                System.err.println("Python脚本错误输出: " + errorOutput);
            }

            // 等待进程完成
            int exitCode = process.waitFor();
            if (exitCode != 0) {
                throw new RuntimeException("Python脚本执行失败，退出码: " + exitCode);
            }

            return result;
        } catch (Exception e) {
            throw new RuntimeException("调用Python简历优化脚本失败", e);
        }
    }

    /**
     * 调用Python面试模拟脚本
     * @param requestData 请求数据
     * @return 处理结果
     */
    public String callInterviewApi(Map<String, Object> requestData) {
        try {
            // 构建Python脚本路径
            // 修改callInterviewApi方法中的脚本路径获取
            String pythonScript = Paths.get(pythonApiConfig.getPythonScriptsPath(), pythonApiConfig.getInterviewScript()).toString();

            // 构建命令参数
            StringBuilder cmdArgs = new StringBuilder();
            for (Map.Entry<String, Object> entry : requestData.entrySet()) {
                cmdArgs.append(" --").append(entry.getKey()).append("=").append(entry.getValue());
            }

            // 执行Python脚本
            String pythonExecutable = "python"; // 考虑使用配置项来设置
            ProcessBuilder processBuilder = new ProcessBuilder(pythonExecutable, pythonScript);

            // 添加命令行参数
            for (Map.Entry<String, Object> entry : requestData.entrySet()) {
                processBuilder.command().add("--" + entry.getKey() + "=" + entry.getValue());
            }

            // 合并标准错误和标准输出
            processBuilder.redirectErrorStream(true);

            // 启动进程
            Process process = processBuilder.start();
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String result = reader.lines().collect(Collectors.joining("\n"));

            // 等待进程完成
            int exitCode = process.waitFor();
            if (exitCode != 0) {
                throw new RuntimeException("Python脚本执行失败，退出码: " + exitCode);
            }

            return result;
        } catch (Exception e) {
            throw new RuntimeException("调用Python面试模拟脚本失败", e);
        }
    }
}