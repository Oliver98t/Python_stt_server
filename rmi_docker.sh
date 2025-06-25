
# add the images you would like to keep 
image_name_keep_list=("whisper-cpp" "postgres" "ubuntu" "python_stt_server-web")

get_image_id()
{   
    local docker_image_name=$1
    docker images --format "{{.Repository}}:{{.Tag}} {{.ID}}" | grep $docker_image_name | awk '{print $2}'
}

mapfile -t image_ids < <(docker images -q)
for id in "${image_ids[@]}"; do
  # check the keep list 
  for image_name in "${image_name_keep_list[@]}"; do
    current_id=$(get_image_id "$image_name")
    if [ "$id" != "$current_id" ]; then
      docker rmi $id
      break
    fi
  done
done
