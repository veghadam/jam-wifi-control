#!/bin/bash
# Check for sensitive data before committing to git

echo "======================================================================"
echo "Checking for Sensitive Data"
echo "======================================================================"
echo

FOUND_ISSUES=0

# Check for common password patterns (but not in examples)
echo "Checking for real passwords..."
if grep -r "password.*=" *.py 2>/dev/null | grep -v "MyPassword" | grep -v "YourPassword" | grep -v "example" | grep -v "#"; then
    echo "⚠️  Found potential real passwords in code"
    FOUND_ISSUES=1
fi

# Check for specific MAC addresses (00:22:6C is HMDX vendor prefix)
echo
echo "Checking for specific MAC addresses..."
if grep -r "00:22:6C:[0-9A-Fa-f:]\{8\}" *.py *.md 2>/dev/null; then
    echo "⚠️  Found specific MAC addresses"
    FOUND_ISSUES=1
fi

# Check for specific local IPs in code (not documentation)
echo
echo "Checking for hardcoded IPs in Python code..."
if grep -r "192\.168\.[0-9]\+\.[0-9]\+" *.py 2>/dev/null | grep -v "example" | grep -v "# " | grep -v '"""' | grep -v "192.168.1.100"; then
    echo "⚠️  Found potentially hardcoded IP addresses in code"
    FOUND_ISSUES=1
fi

# Check if QUICK_START.md (user-specific) would be committed
echo
echo "Checking for user-specific files..."
if [ -f "QUICK_START.md" ] && ! grep -q "QUICK_START.md" .gitignore; then
    echo "⚠️  QUICK_START.md exists but not in .gitignore"
    FOUND_ISSUES=1
fi

# Check for .env files
if ls .env* 2>/dev/null | grep -v ".example"; then
    echo "⚠️  Found .env files that might contain secrets"
    FOUND_ISSUES=1
fi

echo
echo "======================================================================"
if [ $FOUND_ISSUES -eq 0 ]; then
    echo "✅ No sensitive data found! Safe to commit."
    exit 0
else
    echo "⚠️  Potential sensitive data found. Please review above."
    echo
    echo "If these are just examples/documentation, you can ignore this."
    echo "Otherwise, please remove sensitive data before committing."
    exit 1
fi
