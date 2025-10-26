#!/bin/bash

echo "=== Docker Cleanup Script ==="
echo "This will help you free up Docker disk space"
echo

# Show current disk usage
echo "1. Current Docker disk usage:"
docker system df
echo

# Remove unused containers, networks, images, and build cache
echo "2. Cleaning up unused Docker resources..."
docker system prune -a --volumes -f
echo

# Remove old ISP manager images
echo "3. Removing old ISP manager images..."
docker rmi $(docker images | grep "isp-manager" | awk '{print $3}') 2>/dev/null || echo "No old ISP manager images found"
echo

# Remove dangling images
echo "4. Removing dangling images..."
docker image prune -f
echo

# Remove unused volumes
echo "5. Removing unused volumes..."
docker volume prune -f
echo

# Show disk usage after cleanup
echo "6. Docker disk usage after cleanup:"
docker system df
echo

# Optional: Remove all stopped containers
read -p "Do you want to remove all stopped containers? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker container prune -f
    echo "Stopped containers removed."
fi

echo "Cleanup completed!"
