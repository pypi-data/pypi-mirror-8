//  (C) Copyright 2014 Alvaro J. Genial (http://alva.ro)
//  Use, modification and distribution are subject to the Boost Software License, Version 1.0.
//  (See accompanying file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt).

#ifndef AJG_SYNTH_TEMPLATES_PATH_TEMPLATE_HPP_INCLUDED
#define AJG_SYNTH_TEMPLATES_PATH_TEMPLATE_HPP_INCLUDED

#include <ajg/synth/support.hpp>

#include <string>
#include <vector>
#include <cstring>
#include <sys/stat.h>

#include <boost/foreach.hpp>
#include <boost/spirit/include/classic_file_iterator.hpp>

#include <ajg/synth/detail/text.hpp>
#include <ajg/synth/templates/base_template.hpp>

namespace ajg {
namespace synth {
namespace templates {

template <class Engine>
struct path_template : base_template<Engine, boost::spirit::classic::file_iterator<typename Engine::char_type> > {
  public:

    typedef path_template                                                       template_type;
    typedef Engine                                                              engine_type;
    typedef typename path_template::kernel_type                                 kernel_type;
    typedef typename kernel_type::iterator_type                                 iterator_type;
    typedef typename kernel_type::range_type                                    range_type;
    typedef typename engine_type::options_type                                  options_type;
    typedef typename options_type::traits_type                                  traits_type;

    typedef typename traits_type::char_type                                     char_type;
    typedef typename traits_type::size_type                                     size_type;
    typedef typename traits_type::boolean_type                                  boolean_type;
    typedef typename traits_type::string_type                                   string_type;
    typedef typename traits_type::path_type                                     path_type;
    typedef typename traits_type::paths_type                                    paths_type;

    // TODO: source()
    typedef path_type                                                           source_type;
    typedef path_type                                                           key_type;
    typedef std::pair<path_type, struct stat>                                   info_type;

  private:

    typedef detail::text<string_type>                                           text;

  public:

    path_template(path_type const& path, options_type const& options = options_type())
            : source_(path), info_(locate_file(path, options.directories)) {
        if (this->info_.second.st_size == 0) { // Empty file.
            this->reset(options);
        }
        else {
            iterator_type begin(text::narrow(this->info_.first));
            iterator_type end = begin ? begin.make_end() : iterator_type();
            this->reset(begin, end, options, text::quote(this->info_.first, '"'));
        }
    }

  private:

    inline static info_type locate_file(path_type const& path, paths_type const& directories) {
        struct stat stats;

        // First try looking in the directories specified.
        BOOST_FOREACH(path_type const& directory, directories) {
            path_type const& base = detail::text<string_type>::trim_right(directory, text::literal("/"));
            path_type const& full = base + char_type('/') + path;
            if (stat(text::narrow(full).c_str(), &stats) == 0) { // Found it.
                return info_type(full, stats);
            }
        }

        std::string const narrow_path = text::narrow(path);

        // Then try the current directory.
        if (stat(narrow_path.c_str(), &stats) != 0) { // TODO: Use wstat where applicable.
            AJG_SYNTH_THROW(read_error(narrow_path, std::strerror(errno)));
        }

        return info_type(path, stats);
    }

    //
    // Using fopen:
    // if (FILE *const file = std::fopen(filename, "rb")) {
    //     std::fclose(file);
    // }
    // else { throw }

    // Using access:
    // if (access(path.c_str(), R_OK | F_OK) != 0) {
    //    AJG_SYNTH_THROW(read_error(path, std::strerror(errno)));
    // }
    //

  public:

    inline info_type const& info() const { return this->info_; }

    // inline path_type const& source() const { return this->info_.first; }
    inline path_type const& source() const { return this->source_; }

    inline static key_type const key(path_type const& source) { return source; }

    inline boolean_type same(path_type const& path, options_type const& options) const {
        // return this->info_.first == path && this->options().directories == options.directories;
        return this->source_ == path && this->options().directories == options.directories;
    }

    inline boolean_type stale(path_type const& path, options_type const& options) const {
        AJG_SYNTH_ASSERT(this->same(path, options));
        struct stat stats;

        if (stat(text::narrow(this->info_.first).c_str(), &stats) == 0) {
            return this->info_.second.st_mtime < stats.st_mtime
                || this->info_.second.st_size != stats.st_size;
        }

        return true; // File may have been deleted, etc.
    }

  private:

    source_type const source_;
    info_type   const info_;
};

}}} // namespace ajg::synth::templates

#endif // AJG_SYNTH_TEMPLATES_PATH_TEMPLATE_HPP_INCLUDED
