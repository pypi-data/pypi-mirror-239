# -*- encoding: utf-8 -*-
# stub: pact-support 1.20.0 ruby lib

Gem::Specification.new do |s|
  s.name = "pact-support".freeze
  s.version = "1.20.0"

  s.required_rubygems_version = Gem::Requirement.new(">= 0".freeze) if s.respond_to? :required_rubygems_version=
  s.require_paths = ["lib".freeze]
  s.authors = ["James Fraser".freeze, "Sergei Matheson".freeze, "Brent Snook".freeze, "Ronald Holshausen".freeze, "Beth Skurrie".freeze]
  s.date = "2023-10-18"
  s.email = ["james.fraser@alumni.swinburne.edu".freeze, "sergei.matheson@gmail.com".freeze, "brent@fuglylogic.com".freeze, "uglyog@gmail.com".freeze, "bskurrie@dius.com.au".freeze]
  s.homepage = "https://github.com/pact-foundation/pact-support".freeze
  s.licenses = ["MIT".freeze]
  s.required_ruby_version = Gem::Requirement.new(">= 2.0".freeze)
  s.rubygems_version = "3.4.10".freeze
  s.summary = "Shared code for Pact gems".freeze

  s.installed_by_version = "3.4.10" if s.respond_to? :installed_by_version

  s.specification_version = 4

  s.add_runtime_dependency(%q<rainbow>.freeze, ["~> 3.1.1"])
  s.add_runtime_dependency(%q<awesome_print>.freeze, ["~> 1.9"])
  s.add_runtime_dependency(%q<diff-lcs>.freeze, ["~> 1.5"])
  s.add_runtime_dependency(%q<expgen>.freeze, ["~> 0.1"])
  s.add_development_dependency(%q<rspec>.freeze, [">= 2.14", "< 4.0"])
  s.add_development_dependency(%q<rake>.freeze, ["~> 13.0"])
  s.add_development_dependency(%q<webmock>.freeze, ["~> 3.18.1"])
  s.add_development_dependency(%q<pry>.freeze, [">= 0"])
  s.add_development_dependency(%q<fakefs>.freeze, ["~> 2.4.0"])
  s.add_development_dependency(%q<hashie>.freeze, ["~> 5.0"])
  s.add_development_dependency(%q<activesupport>.freeze, [">= 0"])
  s.add_development_dependency(%q<appraisal>.freeze, [">= 0"])
  s.add_development_dependency(%q<conventional-changelog>.freeze, ["~> 1.3"])
  s.add_development_dependency(%q<bump>.freeze, ["~> 0.5"])
end
