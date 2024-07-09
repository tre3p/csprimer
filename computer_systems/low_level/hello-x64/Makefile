run:
	@nasm -fmacho64 $(asm_file_name).asm && \
	ld $(asm_file_name).o -o $(asm_file_name) -macos_version_min 11.0 -L /Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/lib -lSystem -no_pie && \
	./$(asm_file_name)