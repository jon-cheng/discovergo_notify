# Use AWS Lambda Python 3.11 runtime
# FROM public.ecr.aws/lambda/python:3.11
FROM public.ecr.aws/lambda/python:3.11-x86_64
# FROM public.ecr.aws/lambda/python:3.11.2022.05.18.21-x86_64

# Install system dependencies
RUN yum install -y unzip wget tar gzip

# Install Chrome dependencies
RUN yum install -y libX11 libXcomposite libXcursor libXdamage libXext \
    libXi libXtst cups-libs libXScrnSaver libXrandr alsa-lib pango \
    atk at-spi2-atk gtk3 libdrm

# Install Chrome and ChromeDriver
RUN wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip -d /usr/bin/ \
    && chmod +x /usr/bin/chromedriver \
    && rm chromedriver_linux64.zip

# Install Headless Chromium
RUN curl -SL https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-57/stable-headless-chromium-amazonlinux-2.zip > headless-chromium.zip \
    && unzip headless-chromium.zip -d /usr/bin/ \
    && chmod +x /usr/bin/headless-chromium \
    && rm headless-chromium.zip

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy function code
COPY src/discovergo_notify/lambda_function.py .

# Update WebDriverFactory in lambda_function.py to use the binaries
RUN sed -i 's/return webdriver.Chrome(options=options)/options.binary_location = "\/usr\/bin\/headless-chromium"\n        return webdriver.Chrome(executable_path="\/usr\/bin\/chromedriver", options=options)/g' lambda_function.py

# Set Lambda handler
CMD ["lambda_function.lambda_handler"]