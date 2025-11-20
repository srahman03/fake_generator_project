FROM nginx
COPY nginx.conf /etc/nginx/
COPY default.conf /etc/nginx/conf.d/
ENTRYPOINT ["top", "-b"]
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]