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

  def current_user_attributes
    preferred_language = params[:preferredLanguage]
    preferred_language ||= "pt-BR"

    {
      'user_metadata' => {
        "preferredLanguage" => preferred_language
      }
    }
  end
end
