def print_formatted(caption, content_method, filler="=", line_width = 100):
    caption_filler_width = int((line_width - len(caption)) / 2) - 1
    extra_filler_required = (line_width - len(caption)) % 2 == 1

    print_value = f"{filler * caption_filler_width} {caption} {filler * caption_filler_width}"
    if extra_filler_required:
        print_value = print_value + filler

    print(f"\n{print_value}")

    content = content_method()
    if type(content) is str:
        print(content)

    print(f"{filler * line_width}\n")