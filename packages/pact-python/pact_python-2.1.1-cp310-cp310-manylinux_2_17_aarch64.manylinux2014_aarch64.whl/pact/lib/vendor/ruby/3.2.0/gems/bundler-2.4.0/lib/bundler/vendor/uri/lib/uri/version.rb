module Bundler::URI
  # :stopdoc:
  VERSION_CODE = '001200'.freeze
  VERSION = VERSION_CODE.scan(/../).collect{|n| n.to_i}.join('.').freeze
  # :startdoc:
end
