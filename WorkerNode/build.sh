#!/bin/bash

echo
echo "+======================"
echo "| START: LOCUST"
echo "+======================"
echo

echo
echo "LOCUST: Incrementing build number"
echo
cv=`cat version.txt`
nlbn="$(echo $cv | rev | cut -d. -f1 | rev)"
nbn=`echo $nlbn | awk '{$1++; print $0}'`
nb=${cv%.*}"."${nbn}
echo $nb > version.txt

echo 
echo "LOCUST: Inserting new build numbers into dockerfile"
echo
host=`uname -a`
case "${host}" in
    Darwin*)
        esccv=$(echo "${cv}" | sed -e 's/[]$.*[\^]/\\&/g' )
        escnb=$(echo "${nb}" | sed -e 's/[]$.*[\^]/\\&/g' )
        sed -i '' "s/${esccv}/${escnb}/" Dockerfile
        ;;
    *)
        dos2unix ./version.txt
        unix2dos ./version.txt
        esccv=`echo ${cv} | head -c -1 | cut -d' ' -f1`
        escnb=`echo ${nb} | head -c -1 | cut -d' ' -f1`
        echo $esccv
        echo $escnb
        sed -i.bak s/$esccv/$escnb/g Dockerfile
esac

echo 
echo "LOCUST: Building container"
echo
docker build -t graboskyc/mongodb-locust-scale:tsdm .

echo 
echo "LOCUST: Starting container"
echo
docker stop locbldctr
docker rm locbldctr
#docker run -t -i -d -p 8888:8888 --name locbldctr --restart unless-stopped -e token="localdev" graboskyc/mongodb-locust-scale:tsdm

echo
echo "+======================"
echo "| END: LOCUST"
echo "+======================"
echo
