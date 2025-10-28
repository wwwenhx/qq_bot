IMAGE_NAME = napcat-bot
CONTAINER_NAME = napcat-bot

docker-build:
	docker build -t $(IMAGE_NAME) .

# 停止并删除旧容器
docker-stop:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

# 启动容器（依赖 docker-stop，保证干净启动）
docker-run: docker-stop
	docker run -d \
		--name $(CONTAINER_NAME) \
		--env-file .env \
		--network napcat-net \
		$(IMAGE_NAME)

