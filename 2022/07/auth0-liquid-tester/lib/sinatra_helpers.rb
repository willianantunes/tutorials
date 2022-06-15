class CustomSinatraBase < Sinatra::Base
  use Rack::CommonLogger

  configure :development do
    register Sinatra::Reloader
  end

  configure do
    enable :logging
    set :views => Proc.new { File.join(File.expand_path('..', root), 'views') }
    Liquid::Template.register_tag('auth0', Auth0Tag)
  end
end
