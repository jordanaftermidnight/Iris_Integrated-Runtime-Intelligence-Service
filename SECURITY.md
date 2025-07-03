# 🔒 IRIS Security Policy

## 🛡️ **Security Overview**

IRIS is designed with security-first principles to protect users and maintain system integrity.

---

## 🚨 **Reporting Security Vulnerabilities**

If you discover a security vulnerability, please:

1. **DO NOT** create a public issue
2. **Email**: jordanaftermidnight@users.noreply.github.com
3. **Subject**: `IRIS Security Vulnerability Report`
4. **Include**: Detailed description, steps to reproduce, potential impact

We take security seriously and will respond within 48 hours.

---

## 🔐 **Security Best Practices**

### **API Key Management**
- ✅ **DO**: Store API keys in environment variables
- ✅ **DO**: Use `.env` files for local development
- ❌ **DON'T**: Commit API keys to version control
- ❌ **DON'T**: Share API keys in code or documentation

### **Environment Variables**
```bash
# Correct way to set API keys
export GROQ_API_KEY="your_key_here"
export GEMINI_API_KEY="your_key_here"
```

### **Configuration Files**
- Use `*.example.*` files for templates
- Never commit actual configuration with secrets
- Use `.gitignore` to prevent accidental commits

---

## 🚫 **Security Restrictions**

IRIS includes built-in protections against:
- Command injection attacks
- Malicious code execution
- Unauthorized access attempts
- Data exfiltration
- Prompt injection attacks

---

## 🔍 **Security Features**

### **Input Sanitization**
- All user inputs are sanitized before processing
- Command injection prevention
- SQL injection protection (if applicable)

### **Secure Defaults**
- Local processing by default (Ollama)
- Optional cloud providers with explicit consent
- No data logging without permission

### **Integrity Checking**
- File integrity verification
- License compliance monitoring
- Ethical usage enforcement

---

## 🛠️ **For Contributors**

### **Security Requirements**
- All PRs must pass security review
- No hardcoded secrets or credentials
- Follow secure coding practices
- Test for injection vulnerabilities

### **Secure Development**
```bash
# Before committing
git diff --check                    # Check for security issues
iris fix                           # Run auto-fix checks
npm run lint                       # Code quality checks
```

---

## 📋 **Security Checklist**

Before deploying IRIS:
- [ ] API keys stored securely
- [ ] `.gitignore` includes sensitive files
- [ ] No hardcoded credentials in code
- [ ] Environment variables configured
- [ ] Security scanning completed
- [ ] Access controls implemented

---

## 🔄 **Security Updates**

- Security patches are released immediately
- Update IRIS regularly: `iris update`
- Monitor security advisories
- Subscribe to security notifications

---

## 📞 **Security Contact**

**Security Team**: jordanaftermidnight@users.noreply.github.com
**PGP Key**: Available on request
**Response Time**: Within 48 hours

---

## 📜 **Responsible Disclosure**

We follow responsible disclosure practices:
1. Report received and acknowledged
2. Investigation and verification
3. Patch development and testing
4. Coordinated public disclosure
5. Credit to reporter (if desired)

---

**🔒 Security is everyone's responsibility. Thank you for helping keep IRIS secure.**