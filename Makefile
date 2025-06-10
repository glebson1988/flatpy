.PHONY: format lint test check help

# Code formatting
format:
	@echo "🎯 Formatting code..."
	black src/
	isort src/

# Code style checking
lint:
	@echo "🔍 Checking code style..."
	flake8 src/ --max-line-length=88

# Run tests
test:
	@echo "🧪 Running tests..."
	python3 -m unittest discover src/tests -v

# Full check: formatting + linting + tests
check: format lint test
	@echo "✅ All checks passed!"

# Help
help:
	@echo "Available commands:"
	@echo "  format  - Code formatting (black + isort)"
	@echo "  lint    - Code style checking (flake8)"
	@echo "  test    - Run tests"
	@echo "  check   - Full check (format + lint + test)"
	@echo "  help    - Show this help" 
