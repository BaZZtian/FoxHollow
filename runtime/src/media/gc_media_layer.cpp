// SPDX-License-Identifier: MIT
#define _FILE_OFFSET_BITS 64
#include "gc_media_layer.h"
#include <cerrno>
#include <climits>
#include <cstring>
#include <fcntl.h>
#include <limits>
#include <sys/stat.h>
#include <unistd.h>

namespace foxhollow {
GcMediaLayer::~GcMediaLayer() { close(); }
void GcMediaLayer::close() {
    gc_disc_close(&disc_);
    dol_ = {};
    dol_info_ = {};
    if (fd_ >= 0) ::close(fd_);
    fd_ = -1;
}
int GcMediaLayer::read_at(void* context, uint64_t offset, void* data, size_t size) {
    auto* self = static_cast<GcMediaLayer*>(context);
    const auto maximum = static_cast<uint64_t>(std::numeric_limits<off_t>::max());
    if (offset > maximum || size > maximum - offset) return -1;
    auto* bytes = static_cast<unsigned char*>(data);
    while (size != 0) {
        const size_t chunk = size > static_cast<size_t>(SSIZE_MAX)
            ? static_cast<size_t>(SSIZE_MAX) : size;
        const ssize_t count = pread(self->fd_, bytes, chunk, static_cast<off_t>(offset));
        if (count < 0 && errno == EINTR) continue;
        if (count <= 0) return -1;
        const auto actual = static_cast<size_t>(count);
        size -= actual;
        offset += actual;
        bytes += actual;
    }
    return 0;
}
int GcMediaLayer::open(const char* iso_path) {
    close();
    if (!iso_path || !*iso_path) return GC_INVALID;
    fd_ = ::open(iso_path, O_RDONLY | O_CLOEXEC);
    if (fd_ < 0) return GC_IO_ERROR;
    struct stat info{};
    if (fstat(fd_, &info) != 0 || !S_ISREG(info.st_mode) || info.st_size < 0) {
        close();
        return GC_IO_ERROR;
    }
    const GcReader reader{this, static_cast<uint64_t>(info.st_size), read_at};
    int result = gc_disc_open(&disc_, &reader);
    if (result == GC_OK && (disc_.disc_number != 0 ||
        (std::strcmp(disc_.game_id, "GSAP01") != 0 &&
         std::strcmp(disc_.game_id, "GSAE01") != 0))) result = GC_WRONG_GAME;
    if (result == GC_OK) result = gc_disc_dol_info(&disc_, &dol_info_);
    if (result == GC_OK) dol_ = dol_info_.file;
    if (result != GC_OK) close();
    return result;
}
int GcMediaLayer::find(const char* path, GcFile* file) const {
    return gc_disc_find(&disc_, path, file);
}
int GcMediaLayer::read(const GcFile* file, uint64_t offset, void* data, size_t size) const {
    return gc_disc_read(&disc_, file, offset, data, size);
}
}
