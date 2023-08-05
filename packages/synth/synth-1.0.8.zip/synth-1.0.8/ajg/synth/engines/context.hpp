//  (C) Copyright 2014 Alvaro J. Genial (http://alva.ro)
//  Use, modification and distribution are subject to the Boost Software License, Version 1.0.
//  (See accompanying file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt).

#ifndef AJG_SYNTH_ENGINES_BASE_CONTEXT_HPP_INCLUDED
#define AJG_SYNTH_ENGINES_BASE_CONTEXT_HPP_INCLUDED

#include <map>
#include <deque>
#include <utility>

#include <boost/function.hpp>
#include <boost/optional.hpp>
#include <boost/noncopyable.hpp>

#include <ajg/synth/exceptions.hpp>
#include <ajg/synth/detail/find.hpp>
#include <ajg/synth/detail/text.hpp>

namespace ajg {
namespace synth {
namespace engines {

//
// context
////////////////////////////////////////////////////////////////////////////////////////////////////

template <class Value>
struct context : boost::noncopyable {
  public:

    typedef Value                                                               key_type;
    typedef Value                                                               value_type;
    typedef context                                                             context_type;

    typedef typename value_type::range_type                                     range_type;
    typedef typename value_type::sequence_type                                  sequence_type;
    typedef typename value_type::association_type                               association_type;
    typedef typename value_type::arguments_type                                 arguments_type;
    typedef typename value_type::attribute_type                                 attribute_type;
    typedef typename value_type::attributes_type                                attributes_type;
    typedef typename value_type::traits_type                                    traits_type;

    typedef typename traits_type::boolean_type                                  boolean_type;
    typedef typename traits_type::char_type                                     char_type;
    typedef typename traits_type::size_type                                     size_type;
    typedef typename traits_type::integer_type                                  integer_type;
    typedef typename traits_type::floating_type                                 floating_type;
    typedef typename traits_type::number_type                                   number_type;
    typedef typename traits_type::date_type                                     date_type;
    typedef typename traits_type::time_type                                     time_type;
    typedef typename traits_type::datetime_type                                 datetime_type;
    typedef typename traits_type::duration_type                                 duration_type;
    typedef typename traits_type::timezone_type                                 timezone_type;
    typedef typename traits_type::string_type                                   string_type;
    typedef typename traits_type::symbols_type                                  symbols_type;
    typedef typename traits_type::paths_type                                    paths_type;
    typedef typename traits_type::names_type                                    names_type;
    typedef typename traits_type::language_type                                 language_type;
    typedef typename traits_type::format_type                                   format_type;
    typedef typename traits_type::formats_type                                  formats_type;
    typedef typename traits_type::istream_type                                  istream_type;
    typedef typename traits_type::ostream_type                                  ostream_type;

    typedef value_type                                                          data_type;
    typedef struct metadata {
        boolean_type  caseless;
        boolean_type  safe;
        string_type   application;
        timezone_type timezone;
        language_type language;
        boolean_type  localized;
        formats_type  formats;

        metadata() : caseless(false), safe(false), localized(false) {}
    }                                                                           metadata_type;
    typedef void const*                                                         match_type;
    typedef boost::function<void(ostream_type&, context_type&)>                 block_type;
    typedef boost::optional<value_type>                                         change_type;

  private:

    typedef std::map<string_type, std::deque<block_type> >                      blocks_type;
    typedef std::stack<match_type>                                              matches_type;
    typedef std::map<match_type, size_type>                                     cycles_type;
    typedef std::map<match_type, value_type>                                    changes_type;
    typedef detail::text<string_type>                                           text;

  public:

    inline explicit context(data_type const& data, metadata_type const& metadata = metadata_type())
        : data_(data), metadata_(metadata) {}

  public:

    inline void            set  (key_type const& key, value_type const& value) { this->data_.attribute(this->cased(key), value); }
    inline void            unset(key_type const& key) { this->data_.attribute(this->cased(key), attribute_type()); }
    inline attribute_type  get  (key_type const& key) const { return this->data_.attribute(this->cased(key)); }
    inline boolean_type    has  (key_type const& key) const { return detail::contains(this->cased(key), this->keys()); }
    inline attributes_type keys() const { return this->data_.attributes(); }

 // inline data_type&       data()       { return this->data_; }
    inline data_type const& data() const { return this->data_; }
    inline data_type        data(data_type data) { std::swap(data, this->data_); return data; }

    inline boolean_type caseless() const { return this->metadata_.caseless; }
    inline boolean_type caseless(boolean_type caseless) { std::swap(caseless, this->metadata_.caseless); return caseless; }

    inline boolean_type safe() const { return this->metadata_.safe; }
    inline boolean_type safe(boolean_type safe) { std::swap(safe, this->metadata_.safe); return safe; }

    inline string_type application() const { return this->metadata_.application; }
    inline string_type application(string_type application) { std::swap(application, this->metadata_.application); return application; }

    inline timezone_type timezone() const { return this->metadata_.timezone; }
    inline timezone_type timezone(timezone_type timezone) { std::swap(timezone, this->metadata_.timezone); return timezone; }

    inline language_type language() const { return this->metadata_.language; }
    inline language_type language(language_type language) { std::swap(language, this->metadata_.language); return language; }

    inline boolean_type localized() const { return this->metadata_.localized; }
    inline boolean_type localized(boolean_type localized) { std::swap(localized, this->metadata_.localized); return localized; }

    inline formats_type formats() const { return this->metadata_.formats; }
    inline void         formats(formats_type const& formats) {
        BOOST_FOREACH(typename formats_type::value_type const& format, formats) {
            this->format(format.first, format.second);
        }
    }

    inline string_type current() const {
        if (this->current_.empty()) {
            AJG_SYNTH_THROW(std::invalid_argument("not in a block"));
        }
        return this->current_;
    }

    inline string_type current(string_type name) {
        std::swap(name, this->current_);
        return name;
    }

    inline block_type get_block(string_type const& name) const {
        typename blocks_type::const_iterator const it = this->blocks_.find(name);
        return (it == this->blocks_.end() || it->second.empty()) ? block_type() : it->second.front();
    }

    inline block_type pop_block(string_type const& name) {
        if (block_type const b = this->get_block(name)) {
            this->blocks_[name].pop_front();
            return b;
        }
        return block_type();
    }

    inline void push_block(string_type const& name, block_type const& block) {
        this->blocks_[name].push_back(block);
    }

    inline match_type get_match() const {
        BOOST_ASSERT(!this->matches_.empty());
        match_type const match = this->matches_.top();
        BOOST_ASSERT(match);
        return match;
    }

    inline void pop_match() {
        BOOST_ASSERT(!this->matches_.empty());
        this->matches_.pop();
    }

    inline void push_match(match_type const match) {
        this->matches_.push(match);
    }

    inline size_type cycle(match_type const match, size_type const total) {
        size_type const current = detail::find(match, this->cycles_).get_value_or(0);
        this->cycles_[match] = (current + 1) % total;
        return current;
    }

    inline change_type change(match_type const match) const {
        return detail::find(match, this->changes_);
    }

    inline void change(match_type const match, value_type const& value) {
        this->changes_[match] = value;
    }

    inline format_type format(string_type const& name) const {
        if (boost::optional<format_type> const f = detail::find(name, this->metadata_.formats)) {
            return *f;
        }
        AJG_SYNTH_THROW(std::invalid_argument("format: " + text::narrow(name))); // TODO: unknown_format/missing_format
    }

    inline format_type format_or(string_type const& name, format_type const& f) const {
        return detail::find(name, this->metadata_.formats).get_value_or(f);
    }

    inline void format(string_type const& name, format_type const& format, boolean_type const overwrite = true) {
        if (overwrite) {
            this->metadata_.formats[name] = format;
        }
        else {
            this->metadata_.formats.insert(std::make_pair(name, format));
        }
    }

  private:

    inline key_type cased(key_type const& original) const {
        if (!this->caseless()) {
            return original;
        }
        string_type const lowercased = text::lower(original.to_string());

        BOOST_FOREACH(key_type const& key, this->keys()) {
            if (text::lower(key.to_string()) == lowercased) {
                return key;
            }
        }

        return original;
    }

  private:

    data_type     data_;
    metadata_type metadata_;
    string_type   current_;
    blocks_type   blocks_;
    matches_type  matches_;
    cycles_type   cycles_;
    changes_type  changes_;
};

template <class Context>
struct stage : boost::noncopyable {
  public:

    typedef Context                                                             context_type;

    typedef typename context_type::key_type                                     key_type;
    typedef typename context_type::value_type                                   value_type;

    typedef typename value_type::attribute_type                                 attribute_type;
    typedef typename value_type::attributes_type                                attributes_type;
    typedef typename value_type::traits_type                                    traits_type;

    typedef typename traits_type::boolean_type                                  boolean_type;


  private:

    typedef std::map<key_type, attribute_type>                                  previous_type;

  public:

    stage(context_type& context) : context_(context) {}
    stage(context_type& context, key_type const& key, value_type const& value) : context_(context) { this->set(key, value); }
    stage(context_type& context, boolean_type const empty) : context_(context) { if (empty) this->clear(); }

    ~stage() {
        BOOST_FOREACH(typename previous_type::value_type const& kv, this->previous_) {
            if (kv.second) {
                this->context_.set(kv.first, *kv.second);
            }
            else {
                this->context_.unset(kv.first);
            }
        }
    }

  public:

    inline void clear() {
        BOOST_FOREACH(key_type const& key, context_.keys()) {
            this->unset(key);
        }
    }

    inline void unset(key_type const& key) {
        if (!detail::contains(key, this->previous_)) {
            this->previous_[key] = this->context_.get(key);
        }
        this->context_.unset(key);
    }

    inline void set(key_type const& key, value_type const& value) {
        if (!detail::contains(key, this->previous_)) {
            this->previous_[key] = this->context_.get(key);
        }
        this->context_.set(key, value);
    }

  private:

    context_type& context_;
    previous_type previous_;
};

}}} // namespace ajg::synth::engines

#endif // AJG_SYNTH_ENGINES_BASE_CONTEXT_HPP_INCLUDED

