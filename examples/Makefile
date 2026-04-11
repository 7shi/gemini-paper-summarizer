LANGS   := de en eo es fr ja ko zh
TARGET  := 1706.03762v7
TARGETS := $(foreach lang,$(LANGS),$(TARGET)-$(lang).md)
SRCPDF  := $(TARGET).pdf

all: $(TARGETS)

fix:
	uv run fix_for_github.py *.md

$(SRCPDF):
	wget https://arxiv.org/pdf/$(TARGET) -O $@

$(TARGETS): $(TARGET)-%.md: $(SRCPDF)
	uv run gp-summarize $(SRCPDF) -o $@ -l $*
