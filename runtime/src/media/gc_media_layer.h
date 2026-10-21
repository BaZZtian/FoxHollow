// SPDX-License-Identifier: MIT
#pragma once
#include "gc_disc.h"

namespace foxhollow {
// Positional reads keep concurrent streaming independent of a shared seek cursor.
// The caller must join all readers before closing or destroying this object.
class GcMediaLayer final {
public:
    GcMediaLayer() = default;
    ~GcMediaLayer();
    GcMediaLayer(const GcMediaLayer&) = delete;
    GcMediaLayer& operator=(const GcMediaLayer&) = delete;
    int open(const char* iso_path);
    void close();
    int find(const char* path, GcFile* file) const;
    int read(const GcFile* file, uint64_t offset, void* data, size_t size) const;
    const GcDisc& disc() const { return disc_; }
    const GcFile& dol() const { return dol_; }
    const GcDolInfo& dol_info() const { return dol_info_; }
private:
    static int read_at(void*, uint64_t, void*, size_t);
    int fd_ = -1;
    GcDisc disc_{};
    GcFile dol_{};
    GcDolInfo dol_info_{};
};
}
