PARTS = my-boothook.txt my-cloudconfig.txt
combined-userdata.txt: $(PARTS) Makefile
	write-mime-multipart --output=combined-userdata.txt \
	my-boothook.txt:text/x-shellscript \
	my-cloudconfig.txt
