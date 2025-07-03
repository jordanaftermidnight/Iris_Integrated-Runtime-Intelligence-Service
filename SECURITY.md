# 🔒 Iris Security Framework

**Comprehensive Protection Against Unauthorized Usage and Modification**

---

## 🛡️ **Security Overview**

Iris implements multiple layers of security to prevent unauthorized modifications, ensure ethical usage, and protect intellectual property while maintaining functionality for legitimate users.

### **🔍 Core Security Features**

1. **Code Integrity Protection** - Detects unauthorized modifications
2. **License Validation** - Enforces proper commercial licensing
3. **Ethical Usage Monitoring** - Prevents malicious use cases
4. **Usage Analytics** - Tracks and detects anomalous behavior
5. **Runtime Verification** - Continuous security checks

---

## 🔐 **Protection Mechanisms**

### **1. Code Integrity Checker**
```javascript
// Automatically validates core file integrity
- SHA-256 hashing of critical files
- Tamper detection and warnings
- Runtime integrity verification
- Prevents unauthorized code modifications
```

**Protected Files:**
- Core AI routing logic
- Provider implementations
- License validation system
- Main entry points

### **2. License Validation System**
```javascript
// Enforces proper licensing for commercial usage
- Automatic commercial environment detection
- Usage limit enforcement for personal users
- License key validation and verification
- Trial period management
```

**Commercial Detection:**
- CI/CD environment detection
- Production environment indicators
- Server deployment patterns
- Corporate infrastructure markers

### **3. Ethical Usage Enforcement**
```javascript
// Blocks potentially harmful requests
- Malware/virus generation prevention
- Exploitation attempt detection
- Spam/phishing content blocking
- Illegal activity prevention
```

**Prohibited Patterns:**
- Malicious code generation
- Security exploitation attempts
- Harassment or abuse content
- Copyright infringement activities
- Deceptive content creation

### **4. Usage Monitoring**
```javascript
// Tracks usage patterns and detects anomalies
- Request frequency monitoring
- Duplicate request detection
- Suspicious pattern identification
- Automated usage detection
```

**Anomaly Detection:**
- High-frequency requests (potential bots)
- Identical repeated requests (potential spam)
- Suspicious content patterns
- Commercial usage without licenses

---

## ⚖️ **License Enforcement**

### **Personal Use Limits**
- **1,000 requests per month** for personal users
- Automatic usage tracking and enforcement
- Monthly reset cycle
- Clear limit notifications

### **Commercial Detection**
Iris automatically detects commercial usage based on:
- **Environment Variables** (CI=true, NODE_ENV=production)
- **Infrastructure Patterns** (/opt/, /srv/, container environments)
- **Process Context** (Docker, Kubernetes, cloud platforms)
- **Deployment Indicators** (AWS, Azure, GCP, Heroku, Vercel)

### **License Validation**
```bash
# Environment variable method
export IRIS_LICENSE_KEY="your-commercial-license-key"

# License file method
echo "your-license-key" > .iris-license

# Commercial certificate
curl -o iris-commercial.key https://license-server.com/download
```

---

## 🚨 **Security Responses**

### **Integrity Violations**
```
⚠️  Core file modifications detected. System integrity may be compromised.
```
- **Action**: Warning displayed, functionality continues
- **Purpose**: Alert users to potential tampering

### **Ethical Violations**
```
🚫 Request blocked: Potentially unethical usage detected.
```
- **Action**: Request completely blocked
- **Purpose**: Prevent harmful or illegal usage

### **License Violations**
```
🚫 Commercial usage requires valid license.
📧 Contact: jordanaftermidnight@users.noreply.github.com
```
- **Action**: System exit, functionality blocked
- **Purpose**: Enforce proper commercial licensing

### **Usage Limit Exceeded**
```
🚫 Personal usage limit exceeded (1000/1000 requests this month)
```
- **Action**: Requests blocked until monthly reset
- **Purpose**: Maintain fair usage for personal users

---

## 🛠️ **Bypassing Protection (For Development)**

### **Development Mode**
```bash
# Disable security checks for development
export IRIS_DEV_MODE=true
export IRIS_SKIP_INTEGRITY=true
export IRIS_SKIP_LICENSE=true

# Run with reduced security
iris chat "test message" --dev-mode
```

**⚠️ Warning**: Development bypasses should only be used during legitimate development and testing.

### **Debugging Security Issues**
```bash
# Generate integrity report
iris security-report

# Check license status
iris license-status

# View usage analytics
iris usage-report
```

---

## 🔧 **Security Configuration**

### **Environment Variables**
```bash
# Security settings
IRIS_SECURITY_ENABLED=true           # Enable/disable security checks
IRIS_INTEGRITY_CHECK=true            # File integrity validation
IRIS_ETHICAL_FILTER=true             # Ethical usage enforcement
IRIS_LICENSE_VALIDATION=true         # License compliance checking
IRIS_USAGE_MONITORING=true           # Usage pattern tracking

# Thresholds
IRIS_MAX_REQUESTS_PER_MINUTE=20      # Rate limiting
IRIS_MAX_DUPLICATE_REQUESTS=5        # Spam detection
IRIS_ANOMALY_THRESHOLD=0.8           # Sensitivity level
```

### **Security Logging**
```bash
# Log files created automatically
.iris-usage-log          # General usage tracking
.iris-anomalies          # Detected anomalies
.iris-security           # Security events
```

---

## 📋 **Compliance and Auditing**

### **Security Reports**
Generate comprehensive security reports:
```bash
iris security-report --format json > security-audit.json
iris usage-report --period 30d > usage-analysis.txt
```

### **Audit Trail**
- All requests logged with timestamps
- User identification and context
- Security decisions and blocks
- License validation events

### **Data Protection**
- **No sensitive data logging** - Only hashed/truncated content
- **Local storage only** - No data transmitted to external servers
- **User privacy protection** - Personal information not tracked
- **GDPR compliance** - Data minimization and user control

---

## 🚫 **What This Prevents**

### **Unauthorized Modifications**
- ❌ Bypassing license checks
- ❌ Removing security validations
- ❌ Modifying core AI routing logic
- ❌ Disabling ethical filters

### **Malicious Usage**
- ❌ Malware generation requests
- ❌ Exploitation development
- ❌ Spam/phishing content creation
- ❌ Harassment or abuse scenarios

### **Commercial Abuse**
- ❌ Unlimited commercial usage without license
- ❌ Reselling access to Iris services
- ❌ Enterprise deployment without proper licensing
- ❌ API misuse for commercial products

### **System Abuse**
- ❌ Automated scraping or bulk requests
- ❌ DDoS-style usage patterns
- ❌ Resource exhaustion attacks
- ❌ System fingerprinting attempts

---

## 📞 **Security Contact**

**For security-related inquiries:**
- **Email**: jordanaftermidnight@users.noreply.github.com
- **Subject**: `Iris Security - [Issue Type]`
- **Response Time**: 24-48 hours for security issues

**For license compliance:**
- **Email**: jordanaftermidnight@users.noreply.github.com  
- **Subject**: `Commercial License - Iris`

---

## ⚡ **Impact on Performance**

Security checks are designed to be lightweight:
- **Integrity checks**: ~5ms startup overhead
- **Ethical filtering**: ~2ms per request
- **License validation**: ~1ms per request
- **Usage logging**: <1ms per request

**Total overhead**: <10ms per request with full security enabled.

---

**🔒 Iris Security: Protecting intellectual property while enabling ethical AI usage for everyone.**